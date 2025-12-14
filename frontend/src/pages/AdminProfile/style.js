import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { darkPurple } from '../../constants/colors';

const bgPage = '#F5F7FB';
const card = '#FFFFFF';
const border = '#E5E7EB';
const text = '#0F172A';
const muted = '#6B7280';
const accent = darkPurple;
const shadowSm = '0 10px 40px rgba(15, 23, 42, 0.08)';
const shadowSoft = '0 30px 80px rgba(15, 23, 42, 0.06)';

export const Container = styled.div`
  min-height: 100vh;
  background: radial-gradient(120% 60% at 20% 10%, #e9e2ff 0%, rgba(233, 226, 255, 0) 60%),
    radial-gradient(100% 40% at 80% 0%, #d8f5ef 0%, rgba(216, 245, 239, 0) 60%),
    ${bgPage};
  display: flex;
  flex-direction: column;
`;

// HEADER
export const Header = styled.header`
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(14px);
  background: rgba(255, 255, 255, 0.92);
  border-bottom: 1px solid ${border};
  box-shadow: 0 12px 24px rgba(15, 23, 42, 0.04);
`;

export const HeaderContent = styled.div`
  height: 72px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 16px;
`;

export const LogoImage = styled.img`
  height: 34px;
  width: auto;
`;

export const NavMenu = styled.nav`
  display: flex;
  gap: 8px;
  justify-self: center;
  background: rgba(241, 245, 249, 0.6);
  padding: 4px;
  border-radius: 12px;
  border: 1px solid ${border};
`;

export const NavItem = styled(Link)`
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  color: ${(props) => (props.$active ? accent : muted)};
  background: ${(props) => (props.$active ? '#FFFFFF' : 'transparent')};
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s ease;
  box-shadow: ${(props) => (props.$active ? '0 2px 8px rgba(0,0,0,0.04)' : 'none')};

  &:hover {
    color: ${accent};
    background: ${(props) => (props.$active ? '#FFFFFF' : 'rgba(255,255,255,0.5)')};
  }
`;

export const UserProfile = styled(Link)`
  display: flex;
  align-items: center;
  gap: 12px;
  text-align: right;
  border-left: 1px solid ${border};
  padding-left: 16px;
  text-decoration: none;
  cursor: pointer;
  color: inherit;

  &:hover {
    opacity: 0.8;
  }
`;

export const UserName = styled.div`
  font-weight: 800;
  font-size: 13px;
  color: ${text};
  line-height: 1.1;
`;

export const UserRole = styled.div`
  font-size: 12px;
  color: ${muted};
  line-height: 1.1;
`;

export const UserAvatar = styled.img`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
`;

// MAIN
export const MainContent = styled.main`
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 32px 20px 48px;
  display: flex;
  flex-direction: column;
  gap: 24px;

  @media (min-width: 768px) {
    padding: 40px 20px 56px;
    gap: 28px;
  }
`;

export const TopBar = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: ${muted};
`;

export const SectionBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(106, 58, 159, 0.1);
  color: ${accent};
  font-weight: 800;
  font-size: 12px;
  letter-spacing: 0.01em;
  text-transform: uppercase;
`;

export const SectionMeta = styled.span`
  font-size: 13px;
  font-weight: 700;
  color: ${muted};
`;

export const PageHeader = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;

  @media (min-width: 768px) {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
`;

export const PageTitle = styled.h1`
  font-size: 30px;
  color: ${text};
  font-weight: 900;
  margin: 0;
  letter-spacing: -0.03em;

  @media (min-width: 768px) {
    font-size: 34px;
  }
`;

export const ActionRow = styled.div`
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
`;

export const ActionButton = styled.button`
  padding: 10px 14px;
  border-radius: 12px;
  border: 1px solid ${(p) => (p.$primary ? accent : border)};
  background: ${(p) => (p.$primary ? `linear-gradient(120deg, ${accent}, #8b5cf6)` : card)};
  color: ${(p) => (p.$primary ? '#fff' : text)};
  font-weight: 800;
  cursor: pointer;
  box-shadow: ${(p) => (p.$primary ? shadowSm : 'none')};
  transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease;

  &:hover {
    transform: translateY(-1px);
    border-color: ${accent};
  }
`;

export const ProfileCard = styled.div`
  background: ${card};
  border-radius: 24px;
  padding: 32px;
  border: 1px solid ${border};
  box-shadow: ${shadowSoft};
  display: flex;
  flex-direction: column;
  gap: 28px;
  max-width: 920px;
`;

export const ProfileHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid ${border};
`;

export const LargeAvatar = styled.img`
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
`;

export const ProfileInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

export const ProfileName = styled.h2`
  font-size: 24px;
  font-weight: 900;
  color: ${text};
  margin: 0;
`;

export const ProfileRole = styled.span`
  font-size: 14px;
  color: ${muted};
  font-weight: 700;
  background: #f3f4f6;
  padding: 4px 12px;
  border-radius: 99px;
  width: fit-content;
`;

export const MetaRow = styled.div`
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
`;

export const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 700;
  background: ${(props) => (props.$active ? 'rgba(22, 163, 74, 0.1)' : 'rgba(239, 68, 68, 0.1)')};
  color: ${(props) => (props.$active ? '#16a34a' : '#ef4444')};
`;

export const Tag = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 800;
  background: rgba(106, 58, 159, 0.08);
  color: ${accent};
`;

export const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
`;

export const StatCard = styled.div`
  padding: 14px 16px;
  border-radius: 14px;
  border: 1px solid ${border};
  background: ${card};
  box-shadow: ${shadowSm};
  display: flex;
  flex-direction: column;
  gap: 6px;
`;

export const StatLabel = styled.span`
  font-size: 12px;
  font-weight: 700;
  color: ${muted};
`;

export const StatValue = styled.span`
  font-size: 18px;
  font-weight: 900;
  color: ${text};
  letter-spacing: -0.02em;
`;

export const InfoGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 18px;
`;

export const InfoGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

export const Label = styled.label`
  font-size: 12px;
  font-weight: 700;
  color: ${muted};
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

export const Value = styled.div`
  font-size: 16px;
  font-weight: 600;
  color: ${text};
  padding: 12px 16px;
  background: #f8fafc;
  border: 1px solid ${border};
  border-radius: 12px;
`;

export const InlineList = styled.div`
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
`;
