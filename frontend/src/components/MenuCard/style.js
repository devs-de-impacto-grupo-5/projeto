import styled from 'styled-components';
import { darkPurple } from '../../constants/colors';

export const Container = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 18px 20px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.08);
  cursor: pointer;
  transition: transform 0.16s ease, box-shadow 0.16s ease;
  min-height: 110px;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
  }
`;

export const Title = styled.h3`
  font-size: 16px;
  font-weight: 700;
  color: ${darkPurple};
  margin: 0;
  max-width: 70%;
  line-height: 1.35;
`;

export const IconWrapper = styled.div`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.03);
  color: ${(props) => props.color || darkPurple};
`;
